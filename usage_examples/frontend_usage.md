# Library usage example in the Frontend

We provide support in the [ioet-ui-library](https://github.com/ioet/ioet-ui-library) repository to make use of the feature flags in the frontend.


## Requirements
First of all, you will need an NPM token with read access to the `@ioet/ioet-ui-library` package to be able to install the library in your frontend application.
You can ask for help to the UI Standard team for this.

Second, in your backend application, you have to define an endpoint. It can have any URL or HTTP method that you want, but it must return a dictionary with the names of the feature flags and whether they are enabled or not. Like so:
```json
{
    "myFlag": true,
    "myOtherFlag": false,
}
```

The `Toggles` class has a `get_all_toggles` method made for this purpose, so your endpoint will sort of look like this:

```python
import ioet_feature_flag

provider = ioet_feature_flag.YamlToggleProvider('./feature_toggles/feature-toggles.yaml')
toggles = ioet_feature_flag.Toggles(provider)

@router.get("/feature-flags")
async def get_feature_flags():
    return JSONResponse(
        status_code=200,
        content=toggles.get_all_toggles(context=context)
    )
```

If you wish, you can also have a different source of feature flags for the frontend:

```python
provider = ioet_feature_flag.YamlToggleProvider('./feature_toggles/frontend-feature-toggles.yaml')
toggles = ioet_feature_flag.Toggles(provider)
```

## Usage

Once you have installed the `@ioet/ioet-ui-library` package and defined your backend endpoint, you must wrap your app with the `FeatureFlagProvider` context provider, otherwise you are not going to be able to retrieve any feature flags:

```tsx
const yourFunctionToFetchFlags = async (): Promise<Record<string, boolean>> => {
    // Here you do the stuff to get the json from the API endpoint that you made earlier.
    // Remember, this function must return a `Promise` that resolves to a json object that looks like this:
    /*
        {
            "myFlag": true,
            "myOtherFlag": false,
        }
    */
    // Of course, this will depend on how each app makes use of their API clients, but here's a very vage example:
    try {
        const response = await axios.get('/feature-flags');
        return response?.status === 200 ? response?.data : null;
    } catch (error) {
        return {};
    }
}

const YourApp = () => {
  return (
    <FeatureFlagProvider fetchFeatureFlags={yourFunctionToFetchFlags}>
      <App />
    </FeatureFlagProvider>
  )
}
```


## useFeatureFlag hook

It always returns a `boolean` and it receives the name of the feature flag:

```tsx

const YourComponent = () => {
    const isMyFeatureEnabled = useFeatureFlag("myFeature");
    return (
        <>
        ...
        </>
    )
}

```


## useWithFeature hook

As parameters, it receives the name of the feature flag, `whenOn`, and `whenOff`. These two can be any value that you want (functions, strings, integers, components, etc), as long as:
1. They are **not** `booleans`
2. They are the same type
3. They are not an anonymous function that just returns a boolean, like `() => true`

**If these rules don't apply, it will throw an exception**.

The value of the `whenOn` parameter will be returned if the specified feature flag is enabled.
Likewise, the value of the `whenOff` parameter is returned instead if the specified feature flag is disabled.

```tsx
const OldTitle = () => <h1>Old Title</h1>
const NewTitle = () => <h1>New Title</h1>

const YourComponent = () => {
    const MyTitle = useWithFeature('useNewTitle', OldTitle, NewTitle);
    return (
        <>
            <MyTitle />
        </>
    )
}
```

Remember that you are not limited to components, you can use any type value (except booleans):

```tsx
const YourComponent = () => {
    const title = useWithFeature('useNewTitle', "Old Title", "New Title");
    return (
        <>
            <MyTitle title={title} />
        </>
    )
}
```
