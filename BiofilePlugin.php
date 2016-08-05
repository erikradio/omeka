<?php
class BiofilePlugin extends Omeka_Plugin_AbstractPlugin
{
    protected $_hooks = array(
        'install',
        'uninstall',
        'uninstall_message',
        'upgrade',
        'initialize',
    );

    protected $_filters = array(
        'response_contexts',
        'action_contexts',
    );

    private $_elements;


    public function __construct()
    {
        parent::__construct();

        // Set the elements.
        include 'elements.php';
        $this->_elements = $elements;
    }

    /**
     * Install the plugin.
     */
    public function hookInstall()
    {
        // Add the new elements to the Dublin Core element set.
        $elementSet = $this->_db->getTable('ElementSet')->findByName('Biofile');
        foreach ($this->_elements as $key => $element) {
            if (!in_array($element['label'], $this->_dcElements)) {
                $sql = "
                INSERT INTO `{$this->_db->Element}` (`element_set_id`, `name`, `description`)
                VALUES (?, ?, ?)";
                $this->_db->query($sql, array($elementSet->id, $element['label'], $element['description']));
            }
        }
    }

    /**
     * Uninstall the plugin.
     */
    public function hookUninstall()
    {
        // Delete all the elements and element texts.
        $elementTable = $this->_db->getTable('Element');
        foreach ($this->_elements as $element) {
            if (!in_array($element['label'], $this->_dcElements)) {
                $elementTable->findByElementSetNameAndElementName('Biofile', $element['label'])->delete();
            }
        }
    }

    /**
     * Display the uninstall message.
     */
    public function hookUninstallMessage()
    {
        echo __('%sWarning%s: This will remove all the Dublin Core elements added '
        . 'by this plugin and permanently delete all element texts entered in those '
        . 'fields.%s', '<p><strong>', '</strong>', '</p>');
    }


    public function hookUpgrade($args)
    {
        // Drop the unused dublin_core_extended_relationships table.
        if (version_compare($args['old_version'], '2.0', '<')) {
            $sql = "DROP TABLE IF EXISTS `{$this->_db->DublinCoreExtendedRelationship}`";
            $this->_db->query($sql);
        }
    }

    /**
     * Initialize this plugin.
     */
    public function hookInitialize()

    {
        // Add translation.
        add_translation_source(dirname(__FILE__) . '/languages');
    }

    public function filterResponseContexts($contexts)
    {
        $contexts['dc-rdf'] = array('suffix' => 'dc-rdf',
                                    'headers' => array('Content-Type' => 'text/xml'));
        return $contexts;
    }

    public function filterActionContexts($contexts, $args)
    {
        if ($args['controller'] instanceof ItemsController) {
            $contexts['browse'][] = 'dc-rdf';
            $contexts['show'][] = 'dc-rdf';
        }
        return $contexts;
    }

  
    /**
     * Get the dublin core extended elements array.
     *
     * @return array
     */
    public function getElements()
    {
        return $this->_elements;
    }
}
