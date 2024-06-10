from data.connection import query
from data.schemas import UserOut, AmountOut, AccountBalanceOut
from fastapi import HTTPException, status
from re import search
from security.password_hashing import get_password_hash
from data.models import User


def get_account_balance(user_id: int) -> AccountBalanceOut:
    """This function checks account balance of logged user"""
    data = query.table('users').select('amount').eq('id', user_id).execute()

    # convert ORM object to list with dictionary
    balance_list = data.data

    # convert balance_list to dictionary
    balance = balance_list[0]

    # return balance as dictionary
    return AccountBalanceOut(balance=balance['amount'])


def _is_valid_password(password: str) -> tuple[bool, str]:
    """This function checks if a given password meets specific security requirements.
    It returns a boolean indicating the validity of the password and a message detailing the result."""

    if len(password) < 8:
        return False, 'Password length must be more than 8 symbols!'
    if not search(r'[A-Z]', password):
        return False, 'Password must have at least one capital letter!'
    if not search(r'\d', password):
        return False, 'Password must have at least one digit!'
    if not search(r'[+\-*^&]', password):
        return False, 'Password must have at least one special character: (+, -, *, &, ^, …)'

    return True, 'Password is created!'


def _is_valid_email(email: str) -> True | False:
    """This function checks if a given email address is valid based on the presence of '@' and '.' characters."""

    if ('@' and '.') not in email:
        return False
    return True


def create(username: str, password: str, email: str, phone_number: str) -> UserOut | HTTPException:
    """This function creates a new user with the specified username, password, email, and phone number.
    It validates the input data and raises HTTP exceptions if any validation fails."""

    if _find_user_by_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with this email is ALREADY registered!')

    # If phone number is not equal to 10 symbols,
    # it raises error as result of the function (see how function is implemented).
    # Here we check if phone number already exists, it raises error
    if _find_user_by_phone_number(phone_number):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with this phone number is ALREADY registered!')

    if len(username) < 2 or len(username) > 20:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username must be between 2-20 symbols!')

    is_valid_password, is_valid_password_message = _is_valid_password(password)

    if not is_valid_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=is_valid_password_message)

    # hashing the password if is valid
    hashed_password = get_password_hash(password)

    # check if email contains "@" or "."
    if not _is_valid_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email is not valid!')

    try:
        # variable 'data'  will return a ORM object
        data = query.table('users').insert(
            {"username": username, "password": hashed_password, "email": email, "phone_number": phone_number}).execute()

        # convert variable 'data' to list with dictionaries
        data_lst = data.data

        generated_id = int(data_lst[0]['id'])
        created_at = data_lst[0]['created_at']

        return UserOut(id=generated_id, username=username, email=email, phone_number=phone_number,
                       created_at=created_at)

    except Exception as err:
        # create a 'error_message' variable with error details
        error_message = err.details if hasattr(err, 'details') else 'No details available'
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error_message)


def _find_user_by_email(email) -> User | None:
    """This function retrieves a user record from the database by the specified email address.
    It queries the 'users' table for a matching email and returns a User object populated with the user's details if found.
    If no user is found with the given email, the function returns None."""

    # return ORM object
    data = query.table('users').select('id', 'username', 'password', 'email', 'phone_number', 'created_at').eq('email',
                                                                                                               email).execute()

    # convert data ORM object to list with dictionary in it
    data_lst = data.data

    # check if data_lst is empty, if it's empty, that's because user with this email is not found and return none

    if not data_lst:
        return
        # access dictionary from the list
    data_dict = data_lst[0]

    return User(
        id=data_dict['id'],
        username=data_dict['username'],
        password=data_dict['password'],
        email=data_dict['email'],
        phone_number=data_dict['phone_number'],
        created_at=data_dict['created_at']
    )


def _find_user_by_phone_number(phone_number: str) -> User | None:
    """This function retrieves a user record from the database by the specified phone number.
        It queries the 'users' table for a matching phone number and
        returns a User object populated with the user's details if found.
        If no user is found with the given phone number, the function returns None."""

    user_data = query.table('users').select('*').eq('phone_number', phone_number).execute()

    if len(phone_number) != 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Phone number must be EXACTLY 10 symbols!')

    if not user_data.data:
        return

    user = user_data.data[0]

    return User(
        id=user['id'],
        username=user['username'],
        password=user['password'],
        email=user['email'],
        phone_number=user['phone_number'],
        created_at=user['created_at']
    )


def try_login(email: str, password: str) -> User | HTTPException:
    """This function attempts to log in a user with the provided email address and password.
    If the email address or password is invalid,
    it raises an HTTP exception with a 401 Unauthorized status code."""

    # if email is wrong, return none
    user = _find_user_by_email(email)

    # check if user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Email address: {email} is not valid! Please enter a valid email address!')

    # check if password of current user is invalid, raise exception
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Please, enter a valid password!')

    return user


# Function to verify password (you might have this in your password_hashing module)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hashed_password == get_password_hash(plain_password)


def get_logged_user(logged_user_id: int) -> UserOut:
    logged_user_data = query.table('users').select('*').eq('id', logged_user_id).execute()
    logged_user = logged_user_data.data[0]

    return UserOut(id=logged_user['id'], username=logged_user['username'], email=logged_user['email'],
                   phone_number=logged_user['phone_number'], created_at=logged_user['created_at'])


def update_profile(password: str, email: str, phone_number: str, logged_user_id: int) -> str | HTTPException:
    """Updates the profile of the logged-in user with the provided password, email, and phone number.
        It performs validation on the inputs and ensures they are different from the current values.
        If validation passes, it updates the user's credentials in the database. Raises HTTP exceptions
        for invalid inputs or if the new credentials are the same as the current ones."""

    current_user_data = query.table('users').select('*').eq('id', logged_user_id).execute()
    current_user = current_user_data.data[0]
    current_user_password = current_user['password']
    current_user_email = current_user['email']
    current_user_phone_number = current_user['phone_number']

    hashed_pass = get_password_hash(password)

    # validation step
    is_valid_pass = _is_valid_password(password)
    is_valid_email = _is_valid_email(email)

    if is_valid_pass[0] is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=is_valid_pass[1])
    elif is_valid_email is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid email!')
    elif len(phone_number) != 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Phone number must be EXACTLY 10 symbols!')

    # here we will put the credentials to update, and we use it in the update method from query
    change_credentials_dict = {}

    # here we check if current password is different from new password
    if current_user_password != hashed_pass:
        # if is different, we add the new password to the dict
        change_credentials_dict.update(password=hashed_pass)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Choose different password! ')

    if current_user_email != email:
        # if is different, we add the new email to the dict
        change_credentials_dict.update(email=email)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Choose different email! ')

    if current_user_phone_number != phone_number:
        # if is different, we add the new phone_number to the dict
        change_credentials_dict.update(phone_number=phone_number)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Choose different phone_number! ')

    # and finally, we pass our change_credentials_dict to query method update
    (query.table('users').update(change_credentials_dict).eq('id', logged_user_id).execute())

    return 'Credentials updated!'


def get_logged_user(logged_user_id: int) -> UserOut:
    logged_user_data = query.table('users').select('*').eq('id', logged_user_id).execute()
    logged_user = logged_user_data.data[0]

    # it does not show password for security purposes
    return UserOut(id=logged_user['id'], username=logged_user['username'], email=logged_user['email'],
                   phone_number=logged_user['phone_number'], created_at=logged_user['created_at'])
