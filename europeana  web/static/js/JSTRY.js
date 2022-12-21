//js代码
(function(){
        var oImgList = document.getElementsByClassName("img-list")[0],
            aButton = document.getElementsByClassName("btn"),
            aImgLi = document.querySelectorAll(".img-list li"),
            oWidth = parseFloat(getComputedStyle(aImgLi[0]).width),
            oWrap = document.getElementsByClassName("wrap")[0],
            aTab = document.querySelectorAll(".tab-list li");
            len = aImgLi.length,
            index = 0,
            index_ = 0,
            count = 0;;
        function throttle(fn,time){
            var startTime = new Date();
            return function(){
                var time_ = (((new Date() - startTime) >= time) && (count === index));
                if(time_){
                    fn.apply(this);
                    startTime = new Date();
                    setTimeout(function(){
                        count = index;
                    },1000);
                }
            }
        }
        function btnTab(){
            var t = new Date(),
                direction;
            for(var i = 0,tabLen = aTab.length;i < tabLen;i++){
                (function(i){
                    aTab[i].onclick = function(){
                        if((new Date() - t >= 1000) && (count === index)){
                            index_ = index;
                            i - index > 0 ? direction = true : direction = false;
                            if(this.className !== "on"){
                                aTab[index].className = "";
                                if((i - index) === (tabLen - 1)){
                                    aImgLi[len - 1].className = "active";
                                    aImgLi[0].className = "";
                                    oImgList.style.transition = 0 + "s";
                                    oImgList.style.left = -oWidth + "px";
                                    aTab[0].className = "";
                                    index = len - 2;
                                    aImgLi[index].className = "active";
                                    setTimeout(function(){
                                        oImgList.style.transition = 1 + "s";
                                        oImgList.style.left = 0 + "px";
                                    },1000/60);
                                    setTimeout(function(){
                                        aImgLi[len - 1].className = "";
                                    },1000);
                                }
                                else if((i - index) === (1 - tabLen)){
                                    oImgList.style.transition = 1 + "s";
                                    oImgList.style.left = -oWidth + "px";
                                    aTab[len - 2].className = "";
                                    aImgLi[len - 1].className = "active";
                                    index = 0;
                                    aTab[index].className = "on";
                                    setTimeout(function(){
                                        oImgList.style.transition = 0 + "s";
                                        oImgList.style.left = index + "px";
                                        aImgLi[index].className = "active";
                                        aImgLi[len-2].className = "";
                                        aImgLi[len-1].className = "";
                                    },1000);
                                }
                                else{
                                    if(direction){
                                        oImgList.style.left = -oWidth + "px";
                                        oImgList.style.transition = 1 + "s";
                                        setTimeout(function(){
                                            aImgLi[index_].className = "";
                                            oImgList.style.left = 0 + "px";
                                            oImgList.style.transition = 0 + "s";
                                        },1000);
                                    }
                                    else{
                                        oImgList.style.transition = 0 + "s";
                                        oImgList.style.left = -oWidth + "px";
                                        aImgLi[index].className = "active";
                                        setTimeout(function(){
                                            oImgList.style.transition = 1 + "s";
                                            oImgList.style.left = 0 + "px";
                                        },1000/60);
                                        setTimeout(function(){
                                            aImgLi[index_].className = "";
                                        },1000);
                                    }
                                    index = i;
                                    aImgLi[index].className = "active";
                                }
                                this.className = "on";
                                t = new Date();
                                setTimeout(function(){
                                    count = index;
                                },1000);
                            }
                        }
                    }
                })(i);
            }
        }
        function btnPre(){
            index--;
            if(index < 0){
                aImgLi[len - 1].className = "active";
                aImgLi[0].className = "";
                oImgList.style.transition = 0 + "s";
                oImgList.style.left = -oWidth + "px";
                aTab[0].className = "";
                index = len - 2;
                aImgLi[index].className = "active";
                aTab[index].className = "on";
                setTimeout(function(){
                    oImgList.style.transition = 1 + "s";
                    oImgList.style.left = 0 + "px";
                },1000/60);
                setTimeout(function(){
                    aImgLi[len - 1].className = "";
                },1000);
            }
            else{
                oImgList.style.transition = 0 + "s";
                oImgList.style.left = -oWidth + "px";
                aTab[index + 1].className = "";
                aTab[index].className = "on";
                aImgLi[index].className = "active";
                setTimeout(function(){
                    oImgList.style.transition = 1 + "s";
                    oImgList.style.left = 0 + "px";
                },1000/60);
                setTimeout(function(){
                    aImgLi[index + 1].className = "";
                },1000);
            }
        }
        function btnNext(){
            index++;
            oImgList.style.transition = 1 + "s";
            if(index === len-1){
                oImgList.style.left = -oWidth + "px";
                aTab[len - 2].className = "";
                aImgLi[index].className = "active";
                index = 0;
                aTab[index].className = "on";
                setTimeout(function(){
                    oImgList.style.transition = 0 + "s";
                    oImgList.style.left = index + "px";
                    aImgLi[index].className = "active";
                    aImgLi[len-2].className = "";
                    aImgLi[len-1].className = "";
                },1000);
            }
            else{
                oImgList.style.left = -oWidth + "px";
                aTab[index - 1].className = "";
                aTab[index].className = "on";
                aImgLi[index].className = "active";
                setTimeout(function(){
                    oImgList.style.transition = 0 + "s";
                    aImgLi[index - 1].className = "";
                    oImgList.style.left = 0 + "px";
                },1000);
            }
            setTimeout(function(){
                count = index;
            },1000);
        }
        aButton[0].onclick = throttle(btnPre,1000);
        aButton[1].onclick = throttle(btnNext,1000);
        btnTab();
        var timer = setInterval(btnNext,5000);
        oWrap.onmouseover = function(){
            clearInterval(timer);
        }
        oWrap.onmouseout = function(){
            timer = setInterval(btnNext,5000);
        }
    })();
