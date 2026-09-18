from app.roles.dao import RolesDAO


async def init_roles():
    roles = await RolesDAO.find_all()
    if len(roles) == 0:
        await RolesDAO.add(name="Admin")
        await RolesDAO.add(name="User")