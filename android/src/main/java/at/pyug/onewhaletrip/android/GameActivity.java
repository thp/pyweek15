package at.pyug.onewhaletrip.android;

import android.view.View;
import android.view.MotionEvent;

public class GameActivity extends android.app.Activity {
    private class GameView extends android.opengl.GLSurfaceView implements android.opengl.GLSurfaceView.Renderer {
        public float fx = 1.f, fy = 1.f;

        public GameView () {
            super(GameActivity.this);
            setPreserveEGLContextOnPause(true);
            setEGLContextClientVersion(2);
            setRenderer(this);

            final int targetW = 800, targetH = 480;
            getHolder().setFixedSize(targetW, targetH);

            getViewTreeObserver().addOnGlobalLayoutListener(new android.view.ViewTreeObserver.OnGlobalLayoutListener() {
                @Override
                public void onGlobalLayout() {
                    GameView.this.getViewTreeObserver().removeOnGlobalLayoutListener(this);
                    GameView.this.fx = (float)targetW / GameView.this.getWidth();
                    GameView.this.fy = (float)targetH / GameView.this.getHeight();
                }
            });
        }

        public void onSurfaceCreated(javax.microedition.khronos.opengles.GL10 gl,
                javax.microedition.khronos.egl.EGLConfig config) {
            try {
                GameActivity.this.nativeStart(GameActivity.this.getPackageManager().
                        getApplicationInfo(GameActivity.this.getPackageName(), 0).publicSourceDir);
            } catch (Exception e) {
                GameActivity.this.finish();
            }
        }

        public void onSurfaceChanged(javax.microedition.khronos.opengles.GL10 gl, int width, int height) {}

        public void onDrawFrame(javax.microedition.khronos.opengles.GL10 gl) {
            if (!GameActivity.this.nativeRender()) {
                GameActivity.this.finish();
            }
        }

        public boolean onTouchEvent(MotionEvent e) {
            int action = e.getActionMasked();

            if (action == MotionEvent.ACTION_POINTER_DOWN) {
                action = MotionEvent.ACTION_DOWN;
            } else if (action == MotionEvent.ACTION_POINTER_UP) {
                action = MotionEvent.ACTION_UP;
            }

            if (action == MotionEvent.ACTION_DOWN || action == MotionEvent.ACTION_UP || action == MotionEvent.ACTION_CANCEL) {
                int i = e.getActionIndex();
                GameActivity.this.nativeTouch(action, e.getX(i) * fx, e.getY(i) * fy, e.getPointerId(i));
            } else if (action == MotionEvent.ACTION_MOVE) {
                for (int i=0; i<e.getPointerCount(); i++) {
                    GameActivity.this.nativeTouch(action, e.getX(i) * fx, e.getY(i) * fy, e.getPointerId(i));
                }
            }

            return true;
        }
    }

    private GameView mGameView;
    private android.media.SoundPool mSoundPool;
    static { System.loadLibrary("onewhaletrip"); }

    public void onCreate(android.os.Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mSoundPool = (new android.media.SoundPool.Builder()).setMaxStreams(16).build();
        setContentView(mGameView = this.new GameView());
        setVolumeControlStream(android.media.AudioManager.STREAM_MUSIC);
    }

    private void setImmersiveMode() {
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        mGameView.setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION |
              View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_FULLSCREEN |
              View.SYSTEM_UI_FLAG_IMMERSIVE | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY);
    }

    public void onPause() { mGameView.onPause(); mSoundPool.autoPause(); super.onPause(); }
    public void onResume() { super.onResume(); mSoundPool.autoResume(); mGameView.onResume(); setImmersiveMode(); }
    public void onDestroy() { nativeDestroy(); super.onDestroy(); }

    public int load(String filename) throws java.io.IOException {
        return mSoundPool.load(getAssets().openFd(filename), 1);
    }
    public void play(int id) { mSoundPool.play(id, 1.f, 1.f, 0, 0, 1.f); }

    public native void nativeStart(String apk);
    public native boolean nativeRender();
    public native void nativeTouch(int event, float x, float y, int finger);
    public native void nativeDestroy();
}
