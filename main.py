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

    # Iterate through all policies to find what the user has access to
    for policy in enforcer.get_policy():
        role, domain, obj, act = policy
        # Check if user has this role in this domain using enforce directly
        if enforcer.enforce(user, domain, obj, act):
            access_list.append({"resource_type": obj, "action": act, "domain": domain})

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

    # Iterate through all domains and users to check access
    for domain in domains:
        domain_users = []
        for user in enforcer.get_all_subjects():
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