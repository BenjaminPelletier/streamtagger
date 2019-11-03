package com.streamtagger.android_client

import android.app.Activity
import android.app.ProgressDialog.show
import android.os.Bundle
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity
import android.view.Menu
import android.view.MenuItem

import kotlinx.android.synthetic.main.activity_main.*
import android.content.Intent
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import android.os.AsyncTask
import android.util.Log
import androidx.annotation.UiThread


class MainActivity : AppCompatActivity() {
    val CODE_EDIT_SYNC = 8888

    data class MusicSyncRequest(val localPath: String, val query: String)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        setSupportActionBar(toolbar)

        fab.setOnClickListener { view ->
            val i = Intent(this, SyncEditor::class.java)
            startActivityForResult(i, CODE_EDIT_SYNC)
        }
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        // Inflate the menu; this adds items to the action bar if it is present.
        menuInflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        return when (item.itemId) {
            R.id.action_settings -> true
            else -> super.onOptionsItemSelected(item)
        }
    }

    public override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        when (requestCode) {
            CODE_EDIT_SYNC -> {
                if (resultCode == Activity.RESULT_OK) {
                    val local_path = data!!.getStringExtra("local_path")!!
                    val query = data.getStringExtra("query")!!
                    synchronizeMusic(MusicSyncRequest(local_path, query)).execute()
                }
            }
        }
    }

    class synchronizeMusic(val req: MusicSyncRequest) : AsyncTask<Void, Void, String>() {
        override fun doInBackground(vararg params: Void?): String? {
            Log.d("Streamtagger", "Background task executed with " + req.localPath + " -> " + req.query)
            //TODO: query song list and sync
            return null
        }

        override fun onPreExecute() {
            super.onPreExecute()
            // ...
        }

        override fun onPostExecute(result: String?) {
            super.onPostExecute(result)
            // ...
        }
    }
}
