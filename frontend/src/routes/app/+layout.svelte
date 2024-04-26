<!-- <div class="flex items-center"> -->
<div class="grid grid-cols-3 gap-4">
    <div class="drawer lg:drawer-open">
        <input id="my-drawer-2" type="checkbox" class="drawer-toggle" />
        <div class="drawer-content flex flex-col items-center justify-center">
            <label for="my-drawer-2" class="btn drawer-button lg:hidden">메뉴</label>
        </div>

        <div class="drawer-side">
            <label for="my-drawer-2" aria-label="close sidebar" class="drawer-overlay"></label> 
            <ul class="menu p-4 w-80 min-h-full bg-base-200 text-base-content text-xl font-semibold">
                <li><a href="/">홈 화면</a></li>
                <li><a href="/app/re-review">상품평 확인하기</a></li>
                <li><a href="/app/keyword">키워드 검색하기</a></li>
            </ul>
        </div>
    </div>
    <div class="mt-10" id="abc">
        <slot />
    </div>
</div>