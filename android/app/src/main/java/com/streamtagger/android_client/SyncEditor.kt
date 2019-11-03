package com.streamtagger.android_client

import android.content.Intent
import android.os.Bundle
import com.google.android.material.snackbar.Snackbar
import androidx.appcompat.app.AppCompatActivity

import kotlinx.android.synthetic.main.activity_sync_editor.*
import kotlinx.android.synthetic.main.content_sync_editor.*
import androidx.core.app.ComponentActivity
import androidx.core.app.ComponentActivity.ExtraData
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import android.provider.DocumentsContract
import android.R.attr.data
import android.app.Activity
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T
import androidx.core.content.ContextCompat.getSystemService
import android.icu.lang.UCharacter.GraphemeClusterBreak.T


class SyncEditor : AppCompatActivity() {
    val CODE_SELECT_LOCAL_PATH = 9999

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sync_editor)
        setSupportActionBar(toolbar)

        fab.setOnClickListener { view ->
            Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                .setAction("Action", null).show()
        }

        select_folder.setOnClickListener { view ->
            val i = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
            i.addCategory(Intent.CATEGORY_DEFAULT)
            startActivityForResult(Intent.createChooser(i, "Choose local directory"), CODE_SELECT_LOCAL_PATH)
        }

        save.setOnClickListener { view ->
            val data = Intent()
            data.putExtra("local_path", local_path.text)
            data.putExtra("query", query.text.toString())
            setResult(Activity.RESULT_OK, data)
            finish()
        }
    }

    public override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        when (requestCode) {
            CODE_SELECT_LOCAL_PATH -> {
                val uri = data!!.data!!
                val docUri = DocumentsContract.buildDocumentUriUsingTree(
                    uri,
                    DocumentsContract.getTreeDocumentId(uri)
                )
                val path = docUri.toString() // getPath(this, docUri)
                local_path.text = path
            }
        }
    }
}
