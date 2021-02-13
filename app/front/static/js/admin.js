const table = $('#table').DataTable(); // eslint-disable-line new-cap

var fields = ["username", "email", "admin"]

/**
 * Add user to datatable or edit line.
 * @param {mode} mode - Create or edit.
 * @param {properties} properties - Properties of the user.
 */
function addUser(mode, properties) {
  let values = [];
  for (let i = 0; i < fields.length; i++) {
    values.push(`${properties[fields[i]]}`);
  }
  values.push(
    `<button type="button" class="btn btn-info btn-xs"
    onclick="showUserModal('${properties.id}')">Modify</button>`,
    `<button type="button" class="btn btn-danger btn-xs"
    onclick="deleteUser('${properties.id}')">Delete</button>`
  );
  if (mode == 'edit') {
    table.row($(`#${properties.id}`)).data(values);
  } else {
    const rowNode = table.row.add(values).draw(false).node();
    $(rowNode).attr('id', `${properties.id}`);
  }
}

(function() {
  $.ajax({
    type: 'GET',
    url: `/api/users`,
    success: function(properties) {
      console.log(properties);
      if (!properties) {
        alertify.notify('HTTP Error 403: Forbidden', 'error', 5);
      }
      for (let i = 0; i < properties.users.length; i++) {
        addUser('create', properties.users[i]);
      }
      },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      alertify.notify('Error:' + errorThrown, 'error', 5);
    }
  });
})();

/**
 * Display user modal for creation.
 */
function showModal() { // eslint-disable-line no-unused-vars
  $('#showpw').show();
  $('#edit-form').trigger('reset');
  $('#title').text('Add a user');
  $('#edit').modal('show');
}

/**
 * Display user modal for editing.
 * @param {userId} userId - Id of the user to be deleted.
 */
function showUserModal(userId) { // eslint-disable-line no-unused-vars
  $('#edit-form').trigger('reset');
  $('#showpw').hide();
  $.ajax({
    type: 'GET',
    url: `/api/user/${userId}`,
    success: function(properties) {
      console.log(properties);
      if (!properties) {
        alertify.notify('HTTP Error 403: Forbidden', 'error', 5);
      }
      for (const [property, value] of Object.entries(properties.user)) {
        if(property != "admin"){
          $(`#${property}`).val(value);
        }
      }
      document.getElementById("admin").checked = properties.user.admin;
      $('#title').text(`Edit user '${properties.name}'`);
      $('#edit').modal('show');
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      alertify.notify('Error:' + errorThrown, 'error', 5);
    }
  });
}

/**
 * Create or edit user.
 */
function processData() { // eslint-disable-line no-unused-vars
  if ($('#edit-form').parsley().validate()) {
    $.ajax({
      type: 'POST',
      url: `/api/process_user`,
      dataType: 'json',
      data: $('#edit-form').serialize(),
      success: function(user) {
        if (!user) {
          alertify.notify('HTTP Error 403: Forbidden', 'error', 5);
        } else {
          const title = $('#title').text().startsWith('Edit');
          const mode = title ? 'edit' : 'create';
          addUser(mode, user.user);
          const message = `User '${user.user.username}'
          ${mode == 'edit' ? 'edited' : 'created'}.`;
          alertify.notify(message, 'success', 5);
        }
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        alertify.notify('Error:' + errorThrown, 'error', 5);
      }
    });
    $('#edit').modal('hide');
  }
}

/**
 * Delete user.
 * @param {userId} userId - Id of the user to be deleted.
 */
function deleteUser(userId) { // eslint-disable-line no-unused-vars
  $.ajax({
    type: 'GET',
    url: `/api/delete_user/${userId}`,
    success: function(user) {
      if (!user) {
        alertify.notify('HTTP Error 403: Forbidden', 'error', 5);
      } else {
        $(`#${userId}`).remove();
        alertify.notify(`User '${user.user.username}' deleted.`, 'error', 5);
      }
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      alertify.notify('Error:' + errorThrown, 'error', 5);
    }
  });
}
