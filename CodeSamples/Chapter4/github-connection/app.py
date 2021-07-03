import asyncio

from quart import Quart, redirect, render_template, request

from database import user_dal, initialize_database
from forms import UserForm


app = Quart(__name__)
app.config["WTF_CSRF_SECRET_KEY"] = "A SECRET KEY"
app.config["SECRET_KEY"] = "ANOTHER ONE"


@app.before_serving
async def startup():
    await initialize_database()


@app.get("/users")
async def get_all_users():
    async with user_dal() as ud:
        users = await ud.get_all_users()
        return await render_template("users.html", users=users)


@app.route("/create_user", methods=["GET", "POST"])
async def create_user():
    form = UserForm()
    if request.method == "POST" and form.validate():
        async with user_dal() as ud:
            await ud.create_user(form.name.data, form.email.data, form.slack_id.data)
        return redirect("/users")

    return await render_template("create_user.html", form=form)


if __name__ == "__main__":

    app.run()
