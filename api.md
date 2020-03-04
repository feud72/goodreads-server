## 사용자 

### 회원 가입 

#### 요청 

``` 
POST {{API_URL}}/api/v1/accounts/signup 
``` 

| 파라미터 | 파라미터 유형 | 데이터 타입 | 필수 여부 | 설명 | 
| ---------- | ------------- | ----------- | --------- | -------- | 
| `email` | `body` | `string` | ✅ | 이메일 | 
| `password1` | `body` | `string` | ✅ | 비밀번호 | 
| `password2` | `body` | `string` | ✅ | 비밀번호 확인 | 

#### 응답 

| 키 | 데이터 타입 | 설명 | 
| -------------- | ----------- | ------------- | 
| `message` | `string` | 성공시 success | 
| `email` | `string` | 유저의 email | 
| `token` | `string` | 인증 토큰 |

```json
{
"message" : "success",
"email" : "YOUR EMAIL",
"token" : "YOUR ACCESS TOKEN"
}
```
