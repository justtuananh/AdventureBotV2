import { browser } from '$app/environment';
import {register, init, getLocaleFromNavigator, locale} from 'svelte-i18n'

register('en', () => import('../../lang/en/en.json'));
register('vi', () => import('../../lang/vi/vi.json'));

init({
    fallbackLocale: 'en',
    initialLocale: 'vi',
})

localStorage.setItem('lang', 'vi');

