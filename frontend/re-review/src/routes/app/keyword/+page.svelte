<script>
    let searchedKeyword = '';
    let isClicked = false;
    let isSearched = false;
    let responseData;


    const searchKeyword = async () => {
        isSearched = false;
        isClicked = true;

        try {
            const response = await fetch(`http://localhost:8000/keyword?keyword=${searchedKeyword}`);
            if (!response.ok) {
                throw new Error('Failed API Request!');
            }

            responseData = await response.json();
            console.log("responseData: ", responseData);
            isClicked = false;
            isSearched = true;

        } catch (error) {
            console.error(error);
        }
    }
</script>

<div>
    <div>
        <div class="grid grid-cols-5 gap-1 items-center">
          <div class="text-xl font-medium text-center">키워드 검색: </div>
          <label class="input input-bordered flex items-center gap-2 col-span-3">
            <input bind:value={searchedKeyword} type="text" class="grow" placeholder="키워드를 입력하세요."/>
          </label>
          <button class="btn btn-primary col-span-1" on:click={() => searchKeyword()}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-7 h-7 opacity-100"><path fill-rule="evenodd" d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z" clip-rule="evenodd" /></svg>
          </button>
        </div>
      </div>
</div>

{#if isClicked}
<div class="flex justify-center items-center my-32">
    <span class="loading loading-spinner loading-lg"></span>
</div>

{/if}

{#if isSearched}
    {#if responseData.length === 0}
        <div class="flex justify-center items-center my-32">
            <h1 class="text-2xl">검색 결과가 없습니다.</h1>
        </div>
    {:else}
        <div class="overflow-x-auto my-8">
            <table class="table">
            <thead>
                <tr>
                <th></th>
                <th class="text-lg">상품명</th>
                <th class="text-lg">점수</th>
                <th class="text-lg">키워드</th>
                </tr>
            </thead>
            <tbody>
                {#each responseData as item, i}
                <tr class="hover">
                    <th>{i + 1}</th>
                    <td><a href={item.product_url} class="link link-hover" target="_blank">{item.product_name}</a></td>
                    <td>{item.rate}</td>
                    <td>{item.keyword}</td>
                {/each}
            </tbody>
            </table>
        </div>
    {/if}
{/if}