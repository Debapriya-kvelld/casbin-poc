# Casbin Access Control POC

This project demonstrates the implementation of Role-Based Access Control (RBAC) with domain and resource-specific access control using Casbin and FastAPI.

## Project Purpose

The purpose of this POC is to showcase how to:
- Implement access control using Casbin
- Support resource-specific permissions with wildcard capabilities
- Dynamically query user-resource access and resource-user access based on policies
- Support multi-tenancy through domain-based access control

## Features

- API to fetch all resources and actions accessible by a user across domains
- Support for both wildcard (*) and specific resource ID access control
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
curl "http://localhost:8000/api/user-access?user=alice"
```

Example Response:
```json
{
  "user": "alice",
  "access": [
    {
      "resource_type": "property",
      "action": "read",
      "domain": "DomainA",
      "resource_id": "*"
    },
    {
      "resource_type": "property",
      "action": "write",
      "domain": "DomainA",
      "resource_id": "*"
    }
  ]
}
```

### 2. Get Resource Access
Fetches all users who can access a specific resource for a specific action, grouped by domain.

```
GET /api/resource-access?resource_type={type}&action={action}&resource_id={id}
```

Example Request:
```bash
curl "http://localhost:8000/api/resource-access?resource_type=property&action=read&resource_id=prop_1"
```

Example Response:
```json
{
  "resource_type": "property",
  "action": "read",
  "resource_id": "prop_1",
  "access_by_domain": {
    "DomainA": ["alice", "bob"],
    "DomainB": ["carol"]
  }
}
```

## Policy Management

### Adding New Policies
Policies are stored in `casbin_policy.csv`. The file supports two types of rules:

1. Policy Rules:
   ```
   p, role, domain, resource, action, resource_id
   ```
   Examples:
   ```
   p, admin, DomainA, property, read, *        # Wildcard access to all resources
   p, viewer, DomainA, property, read, prop_1  # Access to specific resource
   ```

2. Role Assignments:
   ```
   g, user, role, domain
   ```
   Examples:
   ```
   g, alice, admin, DomainA
   g, bob, viewer, DomainA
   ```

### Policy File Structure
The policy file is organized into sections:
1. Policy definitions (prefixed with 'p')
   - Can use '*' for wildcard access to all resources
   - Can specify exact resource IDs for fine-grained control
2. Role assignments (prefixed with 'g')

Example policy file:
```csv
# Policies with wildcard access
p, admin, DomainA, property, read, *
p, admin, DomainA, meter, write, *

# Policies with specific resource access
p, viewer, DomainA, property, read, prop_1
p, viewer, DomainA, meter, read, device_1

# Role assignments
g, alice, admin, DomainA
g, bob, viewer, DomainA
```

### Access Control Patterns

The system supports several access control patterns:

1. Full Access with Wildcards:
   ```csv
   p, admin, DomainA, property, read, *
   ```
   Grants access to all resources of type 'property' in DomainA

2. Specific Resource Access:
   ```csv
   p, viewer, DomainA, property, read, prop_1
   ```
   Grants access only to resource 'prop_1'

3. Mixed Access Patterns:
   Users can have both wildcard and specific resource access in different domains

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
# Test user access for alice (admin with wildcard access)
curl "http://localhost:8000/api/user-access?user=alice"

# Test user access for bob (viewer with specific resource access)
curl "http://localhost:8000/api/user-access?user=bob"

# Test resource access for specific property
curl "http://localhost:8000/api/resource-access?resource_type=property&action=read&resource_id=prop_1"
```

## Contributing

Feel free to submit issues and enhancement requests! When contributing:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear description of changes
