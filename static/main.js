// main.js

document.addEventListener('DOMContentLoaded', function () {
  const likeButtons = document.querySelectorAll('.like-btn');
  likeButtons.forEach(button => {
    button.addEventListener('click', function () {
      const clubName = button.getAttribute('data-club-name');

      // 发送 AJAX 请求到后端视图
      fetch(`/like-club/${clubName}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ liked: !button.classList.contains('liked') })
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {

            if (button.classList.contains('liked')) {
              button.textContent = 'Like ❤';
              button.classList.remove('liked');
            } else {
              button.textContent = 'Unlike 🖤';
              button.classList.add('liked');
            }
            alert(data.message);
          } else {

            alert(data.error);
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
});


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function openReviewModal(clubName) {
  console.log("Modal opened for club:", clubName);
  // 获取模态框和评论输入框
  var modal = document.getElementById("reviewModal");
  var textarea = document.getElementById("reviewTextarea");

  // 将评论输入框清空
  textarea.value = "";

  // 显示模态框
  modal.style.display = "block";
}

// 关闭模态框
function closeReviewModal() {
  // 获取模态框
  var modal = document.getElementById("reviewModal");
  var textarea = document.getElementById("reviewTextarea");

  // 关闭模态框
  modal.style.display = "none";
  console.log("Modal:", modal);
  console.log("Textarea:", textarea);
}


function submitReview(clubName) {
  // 获取评论内容
  var reviewContent = document.getElementById("reviewTextarea").value;

  // 输出俱乐部名称和评论内容以进行调试
  console.log("Club Name:", clubName);
  console.log("Review Content:", reviewContent);

  // 将评论内容保存到本地存储，以用户名和俱乐部名称为键
  localStorage.setItem("userReview_" + clubName, reviewContent);

  // 提交评论后关闭模态框
  closeReviewModal();
}


document.addEventListener('DOMContentLoaded', function () {
  const reviewButtons = document.querySelectorAll('.review-btn');
  reviewButtons.forEach(button => {
    button.addEventListener('click', function () {
      console.log("Write a Review button clicked");
      const clubName = button.getAttribute('data-club-name');
      console.log("Club Name:", clubName);
      console.log("Submitting review for club:", clubName);
      openReviewModal(clubName);
      // 在这里调用submitReview函数并传递clubName
      submitReview(clubName);
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  console.log("DOM Content Loaded");
  const reviewButtons = document.querySelectorAll('.review-btn');
  reviewButtons.forEach(button => {
    button.addEventListener('click', function () {
      console.log("Write a Review button clicked");
      const clubName = button.getAttribute('data-club-name');
      console.log("Club Name:", clubName);
      openReviewModal(clubName);
    });
  });
});
