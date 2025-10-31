data_users = [
    {"username" : "user premimum name {id}", "email"  : "userp{id}@example.com","accounttype": "premium","description": "Valid user premium", "expected":  {"ui" : "User created successfully!","message":"True", "api": "200"}},
    {"username" : "user basic name {id}", "email"  : "userb{id}@example.com","accounttype": "basic","description": "Valid user basic","expected":  {"ui" : "User created successfully!","message":"True","api": "200"}}
]
data_users_negative = [
    {
        "username" : "",
        "email"  : "userp{id}@test.com",
        "accounttype": "premium",
        "description": "Empty username",
        "expected":  {
            "ui" : "Please fill out this field.",
            "message":"name",
            "api": "200"}
    },
    {
        "username" : "user basic name {id}",
        "email"  : "userb{id}@test.com",
        "description": "Invalid email",
        "accounttype": "basic",
        "expected":  {
            "ui" : "Invalid email domain. Use @example.com.",
            "message":"True",
            "api": "200"
        }
     },
    {
        "username" : "",
        "email"  : "userp{id}@test.com",
        "accounttype": "",
        "description": "Empty account",
        "expected":  {
            "ui" : "Please select an item in the list.",
            "message":"accounttype",
            "api": "200"
        }
    }

]
data_user_pass_message = "User created successfully!"
data_user_email_validation_message = "Invalid email domain. Use @example.com."
data_user_req_field = "All fields are required!"

transactions_postive = [{"userid" : "12345","recipientId":"6789","amount": "1000","type":"transfer","expected":  {"ui" : "Transaction created successfully! [User: ${userId} → Recipient: ${recipientId}, $${amount}]","message":"True","api": "200" } }]
transactions_negative = [
{"userid" : "12345","recipientId":"6789","amount": "-1000","type":"transfer","expected":{"ui" : "All fields are required and amount must be positive!","message":"True","api": "200" } },
{"userid" : "12345","recipientId":"12345","amount": "1000","type":"transfer","expected":{"ui" : "Cannot transfer to the same user!","message":"True","api": "200" } },
{"userid" : "12345","recipientId":"6789","amount": "10001","type":"transfer","expected":{"ui" : "Amount exceeds transfer limit!","message":"True","api": "200" } }   
]

