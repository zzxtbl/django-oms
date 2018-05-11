/**
 * Created by Administrator on 2018/5/11.
 */
// 给图片添加链接
$(document).ready(function() {
    $("p img").each(function() {
        var strA = "<a class='content_img_in' href='" + this.src + "' target='_blank'></a>";
       $(this).wrapAll(strA);
    });
});
// fancybox
$(".content_img_in").click(function(){
    $("p").slideToggle();
}); 
