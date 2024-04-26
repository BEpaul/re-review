<script>
  let productName = '';
  let isClicked = false;
  let isSearched = false;
  let responseData;
  let displayName = '임시임시 상품명';
  const search = async () => {
    isSearched = false;
    isClicked = true;
    console.log(productName);
    try {
        const response = await fetch(`http://localhost:8000/re-review?productName=${productName}`);
        if (!response.ok) {
          throw new Error('Failed API Request!');
        }

        responseData = await response.json();
        console.log("responseData: ", responseData);
        displayName = responseData.productName;
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
      <div class="text-xl font-medium text-center">상품명 검색: </div>
      <label class="input input-bordered flex items-center gap-2 col-span-3">
        <input bind:value={productName} type="text" class="grow" placeholder="상품명을 입력하세요."/>
      </label>
      <button class="btn btn-primary col-span-1" on:click={() => search()}>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="w-7 h-7 opacity-100"><path fill-rule="evenodd" d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z" clip-rule="evenodd" /></svg>
      </button>
    </div>
  </div>
  
  {#if isClicked}
  <div class="flex flex-col max-w-xl gap-4 w-xl my-8">
    <div class="skeleton h-96 w-full"></div>
    <div class="skeleton h-8 w-56"></div>
    <div class="skeleton h-8 w-full"></div>
    <div class="skeleton h-8 w-full"></div>
  </div>
  {/if}
  {#if isSearched}
    <div class="card bg-base-100 max-w-xl shadow-xl my-8 py-4">
      <figure><img src={responseData.imageUrl} alt="상품 이미지" /></figure>
      <div class="card-body">
        <h2 class="card-title">
          {displayName}
          <div class="badge badge-secondary">{responseData.rate}</div>
        </h2>
        <a href={responseData.productUrl} class="link link-hover" target="_blank">상품 페이지로 이동하기</a>
        <div class="card-actions justify-end">
          <div class="badge badge-outline">{responseData.keyword}</div>
        </div>
      </div>
    </div>
  {/if}
</div>