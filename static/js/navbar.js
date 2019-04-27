/**
 * Created by yaoTao on 2018/12/28 0028.
 */

$(function(){
    $(window).scroll(function() {
            let $this = $(this);
            if($this.scrollTop() > $(".hero").outerHeight() - 150) {
                $(".navbar-mine").addClass("bg-dark");
            }else{
                $(".navbar-mine").removeClass("bg-dark");
            }

            $("section").each(function() {
                if($this.scrollTop() >= ($(this).offset().top - $(".navbar-mine").outerHeight())) {
                    $(".smooth-link").parent().removeClass("active");
                    $(".smooth-link[href='#"+$(this).attr("id")+"']").parent().addClass('active');
                }
            });
        });
})