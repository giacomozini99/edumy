window.onload = () => {
    let updateBtns = document.getElementsByClassName('cart-update');

    let loadCommentsBtn = document.getElementById('load-comments');
    let reviewContainer= document.getElementById('review-container');

    let loadQA = document.getElementById('load-qa');
    let qaContainer= document.getElementById('qa-container');

    let publishBtns = document.getElementsByClassName('publish-course');
    const notificationsBtn = document.getElementById('notifications-btn');
    const notifyListElem = document.querySelector('#notify-list');
    const notifyUnreadElem = document.querySelector('.live_notify_badge');

    for(let btn of updateBtns) {
        btn.addEventListener('click', async (e) => {
            const prodId = btn.dataset.product;
            const op = btn.dataset.action;
            await fetch(`../cart/${op}/${prodId}`);

            if (op === 'remove'){
                const priceElement = document.getElementById('tot-price');
                const totPrice = Number(priceElement.innerText);
                const newPrice = totPrice - Number(btn.dataset.price);
                newPrice > 0 ?
                    priceElement.innerText = newPrice.toString() : priceElement.parentElement.innerText = 'The cart is empty...';
            }

            btn.parentElement.parentElement.remove();

        })
    }

    for(let btn of publishBtns) {
        btn.addEventListener('click', async (e) => {
           const courseId = btn.dataset.course;
           await fetch(`${courseId}/publish`);

           document.querySelector('.button-modal').innerText = 'published';
           document.querySelector('.button-modal').classList = 'mr-3 text-success font-weight-bold bg-transparent border-0';
           $('#exampleModal').modal('hide');

        })
    }
    let readNotifications = true
    notificationsBtn.addEventListener('click',async ()=>{
       if(readNotifications){
        const userId = notificationsBtn.dataset.user;
        await fetch(`/${userId}/readNotifications`);
        await fetch(`/%5Einbox/notifications/api/unread_list/?max=5`);
       }else{
           notifyListElem.innerHTML = ''
           notifyUnreadElem.innerText = '0';
       }
       readNotifications = !readNotifications
    })

    notificationsBtn.addEventListener('focusout', async ()=>{
        readNotifications = !readNotifications
        notifyListElem.innerHTML = ''
        notifyUnreadElem.innerText = '0';
    })
    let page = 1;
    if(loadCommentsBtn){

    loadCommentsBtn.addEventListener('click',async ()=>{
        page += 1
        const data = await fetch(`/reviews?page=${page}`)
        const {page_obj, max_page} = await data.json()
        if(page_obj){
            page_obj.forEach(review =>{

                reviewContainer.innerHTML += `<div class="row border-bottom">
                        <ion-icon name="person-circle-outline" style="height: 4.8rem; width: 4.8rem;"></ion-icon>
                        <div class="col">
                            <p>${ review.student }</p>
                            <p class="mr-3">${ review.rating }/5</p>
                            <p class="mr-3">${ review.body }</p>
                        </div>
                    </div>`
            })
        }
        if(max_page)
            loadCommentsBtn.classList.add('d-none')

    })
    }
    if(loadQA){
        loadQA.addEventListener('click',async ()=>{
        page += 1
        const videoId = document.querySelector('#video').dataset.id
        const data = await fetch(`/question-answer?video=${videoId}&page=${page}`)
        const {page_obj, max_page} = await data.json()
        console.log(page_obj)
        if(page_obj){
            page_obj.forEach(qa =>{

                qaContainer.innerHTML += `<div class="accordion" id="accordionQuestionAnswer{{answer.id}}">
            <div class="card">
                <div class="card-header" id="question{{ question.id}}">
                    <p class="container-fluid font-weight-bold d-flex align-items-center" type="button" class="card-link" data-toggle="collapse" data-target="#answer{{answer.id}}" aria-expanded="false">
                        ${ qa[0].body }
                    </p>
                </div>

                <div id="answer{{answer.id}}" class="collapse show" data-parent="#accordionQuestionAnswer{{answer.id}}">
                    <div class="card-body">
                        ${ qa[1].body }
                    </div>
                </div>
            </div>
        </div>`
            })
        }
        if(max_page)
            loadQA.classList.add('d-none')

        })
    }
    const delAccountBtn = document.querySelector("#del-account");
    if(delAccountBtn){
       delAccountBtn.addEventListener('click', async ()=>{
           const userID = delAccountBtn.dataset.id;
           await fetch(`/delete-account/${userID}`);
           document.querySelector("#del-modal").dataset.target = ''
           $('#exampleModal').modal('hide');
           document.querySelector('#alert').innerHTML = `<div class="alert alert-danger"> Account deleted successfully! You will be redirected in 3 seconds...</div>`
            setTimeout(()=>document.location.href='/',3000)
       })
    }
}

const my_special_notification_callback = data => {
    const notifyListElem = document.querySelector('#notify-list');
    data.unread_list.forEach(e=>{
        notifyListElem.innerHTML += `<div><button class='dropdown-item' type='button'>${e.description}</button></div>`
    })



}