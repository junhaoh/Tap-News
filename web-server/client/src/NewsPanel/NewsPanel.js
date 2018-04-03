import './NewsPanel.css'
import React, { Component } from 'react'
import _ from 'lodash';
import NewsCard from '../NewsCard/NewsCard'

class NewsPanel extends Component {
    constructor(props) {
        super();
        this.state = {news:null, pageNum:1, loadAll:false};
        this.handleScroll = this.handleScroll.bind(this)
    }

    componentDidMount() {
        this.loadMoreNews()
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000)
        window.addEventListener('scroll', this.handleScroll)
    }

    handleScroll() {
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50)) {
            console.log('load more news')
            this.loadMoreNews()
        }
    }

    loadMoreNews(e) {
        if (this.state.loadAll === true) {
            return
        }

        let url = 'http://localhost:3000/news/userId' + Auth.getEmail() + '/pageNum' + this.state.pageNum

        let request = new Request(encodeURI(url), {
            method: 'GET',
            headers: {
                'Authorization': 'bearer' + Auth.getToken()
            },
            cache: false
        })

        fetch(request)
        .then((res) => res.json())
        .then((news) => {
            if (!news || news.length === 0) {
                this.setState({loadAll: true})
            }

            this.setState({
                news: this.state.news ? this.state.news.concat(news) : news,
                pageNum: this.state.pageNum + 1
            })
        })
    }

    renderNews() {
        const news_list = this.state.news.map(news => {
            return (
                <a className='list-group-item' href='/'>
                    <NewsCard news={news} />
                </a>
            )
        })

        return (
            <div className='container-fluid'>
                <div className='list-group'>
                    {news_list}
                </div>
            </div>
        )
    }

    render() {
        if (this.state.news) {
            return (
                <div>{this.renderNews()}</div>
            )
        } else {
            return (
                <div>
                    <div id='msg-app-loading'>Loading...</div>
                </div>  
            )
        }
    }

}


export default NewsPanel