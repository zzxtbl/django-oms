/**
 * Created by Administrator on 2018/5/11.
 */
// 给图片添加链接
$(document).ready(function() {
    $("p img").each(function() {
        var strA = "<img class='gallery' src='" + this.src + "' data-action='zoom'/>";
        $(this).replaceWith(strA);
    });
});
