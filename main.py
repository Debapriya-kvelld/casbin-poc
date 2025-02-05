from fastapi import FastAPI, HTTPException, Query
import casbin  # type: ignore

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

    # Get unique domains from policies
    policies = enforcer.get_policy()
    domains = {policy[1] for policy in policies}  # domain is at index 1

    # Check permissions for each combination
    for domain in domains:
        for resource_type in resource_types:
            for action in actions:
                # First check if user has wildcard access
                if enforcer.enforce(user, domain, resource_type, action, "*"):
                    access_list.append(
                        {
                            "resource_type": resource_type,
                            "action": action,
                            "domain": domain,
                            "resource_id": "*",
                        }
                    )
                else:
                    # If no wildcard access, check specific resource IDs
                    resource_ids = {
                        policy[4]
                        for policy in policies
                        if policy[2] == resource_type and policy[4] != "*"
                    }
                    for res_id in resource_ids:
                        if enforcer.enforce(user, domain, resource_type, action, res_id):
                            access_list.append(
                                {
                                    "resource_type": resource_type,
                                    "action": action,
                                    "domain": domain,
                                    "resource_id": res_id,
                                }
                            )

    if not access_list:
        raise HTTPException(status_code=404, detail="No access found for the user.")
    return {"user": user, "access": access_list}


@app.get("/api/resource-access")
def get_resource_access(
    resource_type: str = Query(...), action: str = Query(...), resource_id: str = Query("*")
):
    """
    Fetch all users/accounts who can access a specific resource for a specific action across all domains.
    Example:
        GET /api/resource-access?resource_type=property&action=read&resource_id=id_1
    """
    access_by_domain = {}

    # Get all domains from policies
    policies = enforcer.get_policy()
    domains = {policy[1] for policy in policies}  # domain is at index 1

    # Get all role assignments to find actual users
    role_assignments = enforcer.get_grouping_policy()
    users = set(user for user, _, _ in role_assignments)

    # Iterate through all domains and users to check access
    for domain in domains:
        domain_users = []
        for user in users:
            if enforcer.enforce(user, domain, resource_type, action, resource_id):
                domain_users.append(user)
        if domain_users:
            access_by_domain[domain] = domain_users

    if not access_by_domain:
        raise HTTPException(status_code=404, detail="No users have access to this resource.")
    return {
        "resource_type": resource_type,
        "action": action,
        "resource_id": resource_id,
        "access_by_domain": access_by_domain,
    }


@app.get("/")
def root():
    return {"message": "Casbin POC: User and Resource Access Control"}
