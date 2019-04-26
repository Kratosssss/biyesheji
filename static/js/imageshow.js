/**
 * Created by yaoTao on 2018/12/28 0028.
 */

$(function(){
$("#navbar li").on("click",(function() {

    $("#navbar li").removeClass("active");
    $(this).addClass("active");

}))
})