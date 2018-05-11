/**
 * Created by Administrator on 2018/5/11.
 */
// 给图片添加链接
$(document).ready(function() {
    $("p img").each(function() {var strA = "<a id='content_img' href='" + this.src + "'></a>";
    $(this).wrapAll(strA);
    });
});
// fancybox
$("#content_img").fadeOut({
    openEffect    : 'elastic',
    closeEffect   : 'elastic',
});
