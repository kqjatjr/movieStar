(function () {
  class MovieStarList {
    constructor() {
      this.$starList = [];
      this.getStarList();
    }
    initialize() {
      this.$movieStar = document.querySelector("#container");
      this.$renderList = document.querySelector("#favoriteStarList");
      this.setEvents();
      return this.getStarList();
    }

    setEvents() {
      this.$movieStar.addEventListener("click", this.handleClicklikeBtn);
    }

    handleClicklikeBtn = (event) => {
      const buttonID = event.target.getAttribute("data-id");
      console.log(buttonID);
      // const starLikeId = this.$likeBtn.dataset.id;
      // console.log("/api/star/" + starLikeId + "/like");
      // return fetch("/api/star/" + starLikeId + "/like", { method: "PUT" });
    };

    getStarList() {
      return fetch("/api/star/list", { method: "GET" })
        .then((response) => response.json())
        .then(({ stars }) => this.setStarList(stars));
    }
    setStarList(stars) {
      this.$starsList = stars;
      this.renderStarList();
    }
    renderStarList() {
      this.$renderList.innerHTML = this.$starsList
        .map(
          ({ _id, name, img_url, recent, url, like }) => `
            <li>
              <div class="star-list" id="star-box">
                <div class="card">
                  <div class="card-content">
                    <div class="media">
                      <div class="media-left">
                        <figure class="image is-48x48">
                          <img
                            src="${img_url}"
                            alt="Placeholder image"
                          />
                        </figure>
                      </div>
                      <div class="media-content">
                        <a href="${url}"  class="star-name title is-4"
                        >${name} (좋아요: ${like})</a
                        >
                        <p class="subtitle is-6">${recent}</p>
                      </div>
                    </div>
                  </div>
                  <footer class="card-footer">
                    <a class="card-footer-item has-text-info" data-id="${_id}">
                      좋아요!
                      <span class="icon">
                        <i class="fas fa-thumbs-up"></i>
                      </span>
                    </a>
                    <a class="card-footer-item has-text-danger" data-id="${_id}">
                      삭제
                      <span class="icon">
                        <i class="fas fa-ban"></i>
                      </span>
                    </a>
                  </footer>
                </div>
              </div>
            </li>
            `,
        )
        .join("");
    }
  }
  window.MovieStarList = MovieStarList;
})(window);
