const User = require("../models/user.model.js");


exports.create = (req, res) => {
  // Validate request
  
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }

  // Create
  const user = new User({
    user_name: req.body.user_name,
    user_email: req.body.user_email,
    active: req.body.active
  });

  // Save
  User.create(user, (err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while creating the user."
      });
    else res.send(data);
  });
};

// Retrieve all
exports.findAll = (req, res) => {

  User.getAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while retrieving users."
      });
    else res.send(data);
  });
};

// Find a single
exports.findOne = (req, res) => {
  User.findById(req.params.id_users, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found user with id ${req.params.id_users}.`
        });
      } else {
        res.status(500).send({
          message: "Error retrieving user with id " + req.params.id_users
        });
      }
    } else res.send(data);
  });
};

// Update by id
exports.update = (req, res) => {
  // Validate Request
  if (!req.body) {
    res.status(400).send({
      message: "Content can not be empty!"
    });
  }


  User.updateById(
    req.params.id_users,
    new User(req.body),
    (err, data) => {
      if (err) {
        if (err.kind === "not_found") {
          res.status(404).send({
            message: `Not found user with id ${req.params.id_users}.`
          });
        } else {
          res.status(500).send({
            message: "Error updating user with id " + req.params.id_users
          });
        }
      } else res.send(data);
    }
  );
};

// Delete by id
exports.delete = (req, res) => {
  User.remove(req.params.id_users, (err, data) => {
    if (err) {
      if (err.kind === "not_found") {
        res.status(404).send({
          message: `Not found user with id ${req.params.id_users}.`
        });
      } else {
        res.status(500).send({
          message: "Could not delete user with id " + req.params.id_users
        });
      }
    } else res.send({ message: `user was deleted successfully!` });
  });
};

// Delete all
exports.deleteAll = (req, res) => {
  User.removeAll((err, data) => {
    if (err)
      res.status(500).send({
        message:
          err.message || "Some error occurred while removing all users."
      });
    else res.send({ message: `All users were deleted successfully!` });
  });
};
