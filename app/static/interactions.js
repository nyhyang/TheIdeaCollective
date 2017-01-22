$(document).ready(
    $("#comment-btn").on('click', function() {
        
        var comment =  $("#comment").val(); // Get value from the form
        var idea_id = $("#newcomment").attr("name");
        var commenter = $('#comment-btn').attr("value");
        var picture_url = $("#usr-pic").attr("name");
        console.log(picture_url);
        // alert(idea_id);
        // alert($('#idea-owner').text());

        var comment_html = '<li class="collection-item avatar"><img src='+picture_url+'alt="" class="circle"><span class="title">'+commenter+'</span><p>'+comment+'</p></li>';
        $('#comment-container').append(comment_html); //Append comment to DOM

        // Ajax call to write comment to the database

        $.ajax({
          url: '/addcomment',
          type: 'POST',
          data: { data:
            JSON.stringify({
              "comment": comment,
              // "user_id": <>,
              "idea_id": idea_id,
              // "ts": <current_ts>
            })
          },
          success: function() {
              
          }
        });



        $("#comment").val(""); // Clear the form
      
        
    })
);

function sendMail()
{
   var addr= $("#intouch-btn").attr("value");
   var idea_name = $("#idea-name").text();
   console.log(addr);
   console.log(idea_name);
   window.location.href = "mailto:"+addr+"?subject=I liked your idea,"+idea_name;
}

$(".tag-btn").click(function () {
   $(this).toggleClass("#f44336");
});







