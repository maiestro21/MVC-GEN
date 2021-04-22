module.exports = app => {
  const users = require("../controllers/user.controller.js");

  app.post("/users", users.create);

  app.get("/users", users.findAll);

  app.get("/users/:id_users", users.findOne);

  app.put("/users/:id_users", users.update);

  app.delete("/users/:id_users", users.delete);

  app.delete("/users", users.deleteAll);
};
