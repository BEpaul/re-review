<script>
    const goReReview = () => {
        window.location.href = '/app/re-review';
    }

    const goKeyword = () => {
        window.location.href = '/app/keyword';
    }
</script>

<div class="flex justify-center items-center h-screen pb-12">
    <div class="text-center font-bold">
        <h1 class="text-4xl">
            변별 없는 무신사 후기, <br/> 좀 더 똑똑하게 쇼핑하자!
        </h1>

        <div class="grid justify-center my-12 gap-4">
            <button class="btn w-96 text-lg" href="/re-review" on:click={() => goReReview()}>상품평 확인하기</button>
            <button class="btn w-96 text-lg" href="/re-review" on:click={() => goKeyword()}>키워드 검색하기</button>
        </div>
    </div>
</div>
