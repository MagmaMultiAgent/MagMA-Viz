<script>

</script>

<div class="container">
    <img src="/favicon.png" alt="icon" class="icon" >

    <div class="title">
        MagmaViz
        <div class="sub-title">by MagMA</div>
    </div>

    <div class="icons">
        <a href="mailto:m.gergely1999@gmail.com" >
            <img src="/icons/at-512.png" alt="email" class="icon">
        </a>
        <a href="https://github.com/MagmaMultiAgent" target="_blank">
            <img src="/icons/github-mark-white.png" alt="github" class="icon">
        </a>
    </div>

</div>

<style>
    * {
        background-color: dimgray;
        color: white;
    }

    .container{
        width: 100%;
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-bottom: 10px;
        border-bottom: 1px black solid;
        position: relative;
    }

    .icon {
        max-height: 100px;
        width: auto;
        object-fit: contain;
    }

    .title {
        color: #E5AA6B;
        position: relative;
        font-weight: bolder;
        font-size: 30px;
        margin-left: 10px;
        margin-right: 30px;
        text-shadow: 1px 1px BLACK;
        padding-bottom: 17px;
    }

    .sub-title {
        color: #E33F65;
        position: absolute;
        right: 0;
        font-weight: bold;
        font-size: 17px;
        text-shadow: 1px 1px BLACK;
    }

    .icons {
        height: 40px;
        right: 0;
        position: absolute;
        margin-right: 30px;
    }

    .icons img {
        max-height: 40px;
        width: auto;
        object-fit: contain;
        margin-left: 30px;
    }

</style>
