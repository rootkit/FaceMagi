
var shareServices = {};
var init = function() {
	plus.share.getServices(function(services) {
		for(var i = 0, len = services.length; i < len; i++) {
			shareServices[services[i].id] = services[i];
			console.log('--> plus 获取到分享服务：' + services[i].id + ', ' + services[i].description);
		}
	});
};
var isWechatInstalled = function() {
	return plus.runtime.isApplicationExist && plus.runtime.isApplicationExist({
		pname: 'com.tencent.mm',
		action: 'weixin://'
	});
};

function share(id, msg, callback) {
	var service = shareServices[id];
	if(!service) {
		callback && callback(false);
		return;
	}
	var _share = function() {
		service.send(msg, function() {
			plus.nativeUI.toast("分享到\"" + service.description + "\"成功！");
			callback && callback(true);
		}, function(e) {
			plus.nativeUI.toast("分享到\"" + service.description + "\"失败！");
			callback && callback(false);
		})
	};
	if(service.authenticated) {
		_share(service, msg, callback);
	} else {
		service.authorize(function() {
			_share(service, msg, callback);
		}, function(e) {
			console.log("认证授权失败");
			callback && callback(false);
		})
	}
};

function openSystem(msg, callback) {
	if(plus.share.sendWithSystem) {
		plus.share.sendWithSystem(msg, function() {
			//TODO 系统分享暂不支持回调
			//callback && callback(true);
		}, function() {
			//TODO 系统分享暂不支持回调
			//callback && callback(false);
		});
	} else {
		callback && callback(false);
	}
}
var open = function(msg, callback) {
	/**
	 *如下情况直接打开系统分享
	 * 1、未配置微信分享通道
	 * 2、用户手机未安装威胁你
	 * 3、360浏览器下
	 */

	if(shareServices.weixin && isWechatInstalled() && !/360\sAphone/.test(navigator.userAgent)) {
		plus.nativeUI.actionSheet({
			title: '分享到',
			cancel: "取消",
			buttons: [{
				title: "微信消息"
			}, {
				title: "微信朋友圈"
			}, {
				title: "更多分享"
			}]
		}, function(e) {
			var index = e.index;
			switch(index) {
				case 1: //分享到微信好友
					msg.extra = {
						scene: 'WXSceneSession'
					};
					share('weixin', msg, callback);
					break;
				case 2: //分享到微信朋友圈
					msg.title = msg.content;
					msg.extra = {
						scene: 'WXSceneTimeline'
					};
					share('weixin', msg, callback);
					break;
				case 3: //更多分享
					var url = msg.href ? ('( ' + msg.href + ' )') : '';
					msg.title = msg.title + url;
					msg.content = msg.content + url;
					openSystem(msg, callback);
					break;
			}
		})
	} else {
		//系统分享
		var url = msg.href ? ('( ' + msg.href + ' )') : '';
		msg.title = msg.title + url;
		msg.content = msg.content + url;
		openSystem(msg, callback);
	}
};

var plusReady = function(callback) {
	// #ifdef APP-PLUS
	callback();
	// #endif
}
plusReady(init);


module.exports = {
	plusShare: open
}