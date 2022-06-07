package com.example.ch14

import android.Manifest
import android.content.*
import android.content.pm.PackageManager
import android.graphics.BitmapFactory
import android.os.Build
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.provider.MediaStore
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AlertDialog
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.ch14.databinding.ActivityMainBinding
import com.google.android.material.snackbar.Snackbar

class MainActivity : AppCompatActivity() {
    private val binding by lazy { ActivityMainBinding.inflate(layoutInflater) }
    private val adapter by lazy { MyAdapter(viewModel) }
    private val broadcastReceiver = MyBroadcastReceiver()
    private val viewModel by viewModels<MyViewModel>()

    private fun requestSinglePermission(permission: String) {
        if (checkSelfPermission(permission) == PackageManager.PERMISSION_GRANTED)
            return

        val requestPermLauncher =
            registerForActivityResult(ActivityResultContracts.RequestPermission()) {
                if (it == false) { // permission is not granted!
                    AlertDialog.Builder(this).apply {
                        setTitle("Warning")
                        setMessage(getString(R.string.no_permission, permission))
                    }.show()
                }
            }

        if (shouldShowRequestPermissionRationale(permission)) {
            // you should explain the reason why this app needs the permission.
            AlertDialog.Builder(this).apply {
                setTitle("Reason")
                setMessage(getString(R.string.req_permission_reason, permission))
                setPositiveButton("Allow") { _, _ -> requestPermLauncher.launch(permission) }
                setNegativeButton("Deny") { _, _ -> }
            }.show()
        } else {
            // should be called in onCreate()
            requestPermLauncher.launch(permission)
        }
    }

    private fun hasPermission(perm: String) =
        checkSelfPermission(perm) == PackageManager.PERMISSION_GRANTED

    private fun readMedia() {
        println("readMedia!")
        var count = 0
        do {
            println("+++++++++++++++++++++++++++")
            println("count: ${++count}")
            println("+++++++++++++++++++++++++++")

            val collection = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                MediaStore.Images.Media.getContentUri(MediaStore.VOLUME_EXTERNAL)
            } else {
                MediaStore.Images.Media.EXTERNAL_CONTENT_URI
            }

            val projection =
                arrayOf(MediaStore.Images.ImageColumns._ID, MediaStore.Images.ImageColumns.TITLE)
            val cursor = contentResolver.query(collection, projection, null, null, null)
            cursor?.apply {
                val idCol = getColumnIndex(MediaStore.Images.ImageColumns._ID)
                val titleCol = getColumnIndex(MediaStore.Images.ImageColumns.TITLE)

                while (moveToNext()) {
                    val contentUri = ContentUris.withAppendedId(
                        collection,
                        getLong(idCol)
                    )
                    val title = getString(titleCol)
                    val bitmap = contentResolver.openInputStream(contentUri)?.use {
                        BitmapFactory.decodeStream(it)
                    }
                    adapter.addItem(Item(bitmap, title))
                }
                close()
            }
        } while (!hasPermission(Manifest.permission.READ_EXTERNAL_STORAGE))
    }

    private fun startBroadcastReceiver() {
        IntentFilter().also {
            it.addAction(ACTION_MY_BROADCAST)
            registerReceiver(broadcastReceiver, it)
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)

        binding.recyclerView.adapter = adapter
        binding.recyclerView.layoutManager = LinearLayoutManager(this)
        binding.recyclerView.setHasFixedSize(false)

        startBroadcastReceiver()

        requestSinglePermission(Manifest.permission.READ_EXTERNAL_STORAGE)

//        requestMultiplePermission(
//            arrayOf(
//                Manifest.permission.READ_EXTERNAL_STORAGE
//            )
//        )
        readMedia()
    }

    override fun onStop() {
        super.onStop()
        unregisterReceiver(broadcastReceiver)
    }

    inner class MyBroadcastReceiver : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            when (intent?.action) {
                ACTION_MY_BROADCAST -> {
                    showBroadcast(ACTION_MY_BROADCAST)
                }
                else -> {
                    showBroadcast(intent?.action ?: "NO ACTION")
                }
            }
        }

        private fun showBroadcast(msg: String) {
            println(msg)
            Snackbar.make(binding.root, msg, Snackbar.LENGTH_SHORT).show()

            binding.textViewBroadcast.text = msg
        }
    }

    companion object {
        const val ACTION_MY_BROADCAST = "ACTION_MY_BROADCAST"
    }
}