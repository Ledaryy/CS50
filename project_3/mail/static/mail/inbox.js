document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
  
  // check is the compose submitted
  document.querySelector("#compose-form").onsubmit = function () {
    event.preventDefault(); // prevents default refresh
    fetch("/emails", {
      method: "POST",
      body: JSON.stringify({
        recipients: document.querySelector("#compose-recipients").value,
        subject: document.querySelector("#compose-subject").value,
        body: document.querySelector("#compose-body").value,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        // Print result
        console.log(result);
        load_mailbox("sent"); // loading "sent" box
        
      });
  };
  
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#email-click-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-click-view").style.display = "none";

  // Show the mailbox name
  document.querySelector("#emails-view").innerHTML = `<h3>${
    mailbox.charAt(0).toUpperCase() + mailbox.slice(1)
  }</h3>`;

  // to make it more simple, I made another function
  if (mailbox === "inbox") {
    fetch_mail_by_folder("inbox")
  }
  if (mailbox === "sent") {
    fetch_mail_by_folder("sent")
  }
  if (mailbox === "archive") {
    fetch_mail_by_folder("archive")
  }



}


function fetch_mail_by_folder(folder) {
  // fetches email by folder name
  fetch(`/emails/${folder}`)
      .then((response) => response.json())
      .then((emails) => {
        emails.forEach(email => {
          // creating an element
          const element = document.createElement("div");
          element.innerHTML = `<div class="container-1">
          <div class="sender"> From: ${email.sender} </div>
          <div class="subject"> Subject: ${email.subject} </div>
          <div class="timestamp"> Time: ${email.timestamp} </div>
          </div>`;
          element.addEventListener("click", function () {
            get_email(email.id, folder);
          });
          element.id = "email-box";
          // working with baground color
          if (email.read == true) { element.style.backgroundColor = "#CDCDCD"} else {
            element.style.backgroundColor = "white"
          }
          const div = document.querySelector('#emails-view')
          div.append(element);

        })
        
      });
}

function reply_to_email(email) {
  // reply button function
  compose_email();
  document.querySelector("#compose-recipients").value = email.sender;
  const reply_subject = document.querySelector("#compose-subject")
  // if nessesary adding Re: to the begining
  if (email.subject.includes("Re:")){ 
    reply_subject.value = email.subject;
  } else {
    reply_subject.value = `Re: ${email.subject}`;
  }
  document.querySelector("#compose-body").value = 
  `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
}

function mark_unmark_email_as_archived(id) {
// marking email as archived, if email already was archived, unmark it
  fetch(`/emails/${id}`)
  .then((response) => response.json())
  .then(email => {
    if (email.archived == true) {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: false
        })
        }).then(() => {
          load_mailbox("inbox"); // when finished, loading inbox
      })
    } else {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: true
        })
        }).then(() => {
          load_mailbox("inbox"); // when finished, loading inbox
      })
    }
  })


  
}

function get_email(id, folder) {
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      
      // hide everything except email click view
      document.querySelector("#emails-view").style.display = "none";
      document.querySelector("#email-click-view").style.display = "block";

      // updating email content
      const element = document.querySelector("#email-click-view");
      element.innerHTML = `
            <div class="form-group">
                From: <input disabled class="form-control" value="${email.sender}">
            </div>
            <div class="form-group">
                To: <input disabled class="form-control" value="Me (${email.recipients})">
            </div>
            <div class="form-group">
                Subject: <input disabled class="form-control" value="${email.subject}">
            </div>
            <div class="form-group">
                Time: <input disabled class="form-control" value="${email.timestamp}">
            </div>
            <div> Content </div>
            <textarea disabled class="form-control" placeholder="${email.body}"></textarea>
                         
      `;
      
      // removing the buttons in "sent" folder
      if (folder !== "sent"){
        const button = document.createElement("div");
        if (email.archived == true) {
          button.innerHTML = `<button class="btn btn-success" id="archive_email_${email.id}">UnArchive</button>`
        }
        if (email.archived == false) {
          button.innerHTML = `<button class="btn btn-secondary" id="archive_email_${email.id}">Archive</button>
          <button class="btn btn-dark" id="reply_email_${email.id}">Reply</button>`
        }
        // adding buttons to the DOM
        element.append(button);
        document.querySelector(`#archive_email_${email.id}`).addEventListener("click", function (){
            mark_unmark_email_as_archived(email.id);
        })
        document.querySelector(`#reply_email_${email.id}`).addEventListener("click", function (){
            reply_to_email(email);
        })
      }

      // mark email as "read"
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })

  });
}