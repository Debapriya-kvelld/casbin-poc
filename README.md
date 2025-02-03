# Casbin Access Control POC

This project demonstrates the implementation of Role-Based Access Control (RBAC) with domain and resources support using Casbin and FastAPI.

## Project Purpose

The purpose of this POC is to showcase how to:
- Implement access control using Casbin
- Dynamically query user-resource access and resource-user access based on policies
- Support multi-tenancy through domain-based access control

## Features

- API to fetch all resources and actions accessible by a user
- API to fetch all users/accounts with access to a specific resource and action
- Support for role inheritance within domains
- Flexible policy management through CSV files

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### 1. Get User Access
Fetches all resources and actions a user has access to.

```
GET /api/user-access?user={username}
```

Example Response:
```json
{
  "user": "Alice",
  "access": [
    {"resource_type": "property", "action": "read", "domain": "OrgA"},
    {"resource_type": "meter", "action": "write", "domain": "OrgA"}
  ]
}
```

### 2. Get Resource Access
Fetches all users who can access a specific resource for a specific action.

```
GET /api/resource-access?resource_type={type}&action={action}&domain={domain}
```

Example Response:
```json
{
  "resource_type": "property",
  "action": "read",
  "domain": "OrgB",
  "users": ["Bob"]
}
```

## Policy Management

### Adding New Policies
Policies are stored in `casbin_policy.csv`. The file supports two types of rules:

1. Policy Rules:
   ```
   p, role, domain, resource, action
   ```
   Example: `p, admin, OrgA, property, read`

2. Role Assignments:
   ```
   g, user, role, domain
   ```
   Example: `g, Alice, admin, OrgA`

### Extending Functionality

To add new resources or actions:
1. Add new policy rules to `casbin_policy.csv`
2. No code changes required unless you need to add new types of permissions

To modify the access control model:
1. Edit the `casbin.conf` file
2. Update the matcher rule if needed

## Security Considerations

- The policy file should be properly secured and backed up
- Consider implementing policy persistence in a database for production use
- Implement proper authentication before the authorization layer
- Regularly audit access patterns and permissions

## Contributing

Feel free to submit issues and enhancement requests!
