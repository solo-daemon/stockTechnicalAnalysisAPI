# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from dotenv import load_dotenv
# import os


# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token")
#         return {"user_id": user_id}
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token validation failed")

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     return verify_token(token)