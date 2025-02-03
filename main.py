from fastapi import FastAPI, HTTPException, Query
import casbin

app = FastAPI()

# Initialize Casbin
enforcer = casbin.Enforcer("casbin.conf", "casbin_policy.csv")


@app.get("/api/user-access")
def get_user_access(user: str):
    """
    Fetch all resources and actions a user has access to.
    Example:
        GET /api/user-access?user=Alice
    """
    access_list = []
    
    # Define common resource types and actions to check for wildcard permissions
    resource_types = ["property", "meter"]
    actions = ["read", "write"]
    domains = set(domain for _, domain, _, _ in enforcer.get_policy())
    
    # Check permissions for each combination
    for domain in domains:
        for resource_type in resource_types:
            for action in actions:
                if enforcer.enforce(user, domain, resource_type, action):
                    access_list.append({
                        "resource_type": resource_type,
                        "action": action,
                        "domain": domain
                    })

    if not access_list:
        raise HTTPException(status_code=404, detail="No access found for the user.")
    return {"user": user, "access": access_list}


@app.get("/api/resource-access")
def get_resource_access(
    resource_type: str = Query(...), action: str = Query(...)
):
    """
    Fetch all users/accounts who can access a specific resource for a specific action across all domains.
    Example:
        GET /api/resource-access?resource_type=property&action=read
    """
    access_by_domain = {}

    # Get all domains from policies
    domains = set(domain for _, domain, _, _ in enforcer.get_policy())

    # Get all role assignments to find actual users
    role_assignments = enforcer.get_grouping_policy()
    users = set(user for user, _, _ in role_assignments)

    # Iterate through all domains and users to check access
    for domain in domains:
        domain_users = []
        for user in users:
            if enforcer.enforce(user, domain, resource_type, action):
                domain_users.append(user)
        if domain_users:
            access_by_domain[domain] = domain_users

    if not access_by_domain:
        raise HTTPException(status_code=404, detail="No users have access to this resource.")
    return {
        "resource_type": resource_type,
        "action": action,
        "access_by_domain": access_by_domain
    }


@app.get("/")
def root():
    return {"message": "Casbin POC: User and Resource Access Control"} 