# Casbin Access Control POC

This project demonstrates the implementation of Role-Based Access Control (RBAC) with domain and resources support using Casbin and FastAPI.

## Project Purpose

The purpose of this POC is to showcase how to:
- Implement access control using Casbin
- Dynamically query user-resource access and resource-user access based on policies
- Support multi-tenancy through domain-based access control

## Features

- API to fetch all resources and actions accessible by a user across domains
- API to fetch all users/accounts with access to a specific resource and action, grouped by domain
- Support for role inheritance within domains
- Flexible policy management through CSV files

## Project Setup

### Prerequisites
- Python 3.12 or higher
- UV package manager (https://github.com/astral-sh/uv)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd casbin-poc
   ```

2. Initialize the project with UV:
   ```bash
   uv init
   ```

3. Install dependencies:
   ```bash
   uv sync
   ```

4. Run the application:
   ```bash
   uv run uvicorn main:app --reload
   ```

The API will be available at http://127.0.0.1:8000

## API Endpoints

### 1. Get User Access
Fetches all resources and actions a user has access to across all domains.

```
GET /api/user-access?user={username}
```

Example Request:
```bash
curl "http://localhost:8000/api/user-access?user=Alice"
```

Example Response:
```json
{
  "user": "Alice",
  "access": [
    {"resource_type": "property", "action": "read", "domain": "OrgA"},
    {"resource_type": "meter", "action": "write", "domain": "OrgA"},
    {"resource_type": "property", "action": "read", "domain": "OrgB"}
  ]
}
```

### 2. Get Resource Access
Fetches all users who can access a specific resource for a specific action, grouped by domain.

```
GET /api/resource-access?resource_type={type}&action={action}
```

Example Request:
```bash
curl "http://localhost:8000/api/resource-access?resource_type=property&action=read"
```

Example Response:
```json
{
  "resource_type": "property",
  "action": "read",
  "access_by_domain": {
    "OrgA": ["Alice"],
    "OrgB": ["Bob", "Alice"]
  }
}
```

## Policy Management

### Adding New Policies
Policies are stored in `casbin_policy.csv`. The file supports two types of rules:

1. Policy Rules:
   ```
   p, role, domain, resource, action
   ```
   Examples:
   ```
   p, admin, OrgA, property, read
   p, analyst, OrgB, property, read
   ```

2. Role Assignments:
   ```
   g, user, role, domain
   ```
   Examples:
   ```
   g, Alice, admin, OrgA
   g, Alice, analyst, OrgB
   ```

### Policy File Structure
The policy file is organized into two sections:
1. Policy definitions (prefixed with 'p')
2. Role assignments (prefixed with 'g')

Example policy file:
```csv
# Policies
p, admin, OrgA, property, read
p, admin, OrgA, meter, write

# Role assignments
g, Alice, admin, OrgA
g, Bob, analyst, OrgB
```

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
- Keep the Casbin model file (`casbin.conf`) and policy file (`casbin_policy.csv`) in a secure location

## Testing

You can test the API endpoints using curl or any HTTP client:

```bash
# Test user access for Alice
curl "http://localhost:8000/api/user-access?user=Alice"

# Test resource access for property read permission
curl "http://localhost:8000/api/resource-access?resource_type=property&action=read"
```

## Contributing

Feel free to submit issues and enhancement requests! When contributing:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear description of changes
