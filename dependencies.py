from typing import Annotated
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from database import supabase
from security import decode_access_token
from models.user_models import UserResponse

bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    scheme_name="JWT Bearer"
)

def get_current_user(credentials:Annotated[HTTPAuthorizationCredentials,Depends(bearer_scheme)]) -> UserResponse:
    token = credentials.credentials    # in sceheme name there is a variable named credentials which has the the token
    user_id = decode_access_token(token)
    try:
        user_response = ( 
            supabase.table("users").select("id,full_name,email,role,is_active,created_at").eq("id",user_id).execute()
        )
    except HTTPException as error:
        print("User lookup error:",error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Unable to retrieve current user"
        )

    if not user_response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail="User account not found",
            headers={
                "WWW-Authenticate":"Bearer"
            }
        )
    user_data = user_response.data[0]

    if not user_data['is_active']:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,detail="User Account is Inactive"
        )
    return UserResponse.model_validate(user_data)       # as user_data is dictionary not an iinstance of current user

CurrentUser = Annotated[UserResponse,Depends(get_current_user)]

def require_admin(current_user: CurrentUser) -> UserResponse:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin permission required"
        )
    return current_user


CurrentAdmin = Annotated[UserResponse,Depends(require_admin)]

